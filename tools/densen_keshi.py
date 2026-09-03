# -*- coding: utf-8 -*-
"""電線消し：空に写り込んだ細い線（電線・アンテナ線）だけを消す。
   ①空の範囲を決める（明るくて青い・上のほう）②その中の細くて暗い筋だけを拾う
   ③その筋だけを塗り直す。建物・窓枠・木には触らない（空の中だけを対象にするため）。
   使い方: python3 tools/densen_keshi.py 入力.jpg 出力.jpg [--check]
   --check を付けると、消した面積の割合だけ出して保存しない。"""
import sys, cv2, numpy as np

def sora_mask(bgr):
    """空とみなす範囲。空だけを取り、白い壁・黒い外壁を巻き込まない。
       ①「空の芯」を厳しく取る（青が赤より十分強い・明るい・のっぺりしている）
       ②電線ぶんの細い隙間だけを埋め直す（芯は電線の所で切れているため）
       ③埋め直した所も、色が空寄りでなければ捨てる（黒い外壁を飲まないため）
       ④画像の上端からつながっている塊だけ残す"""
    b,g,r = cv2.split(bgr.astype(np.int16))
    lum = bgr.mean(axis=2)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    mu = cv2.blur(gray,(9,9))
    sd = cv2.sqrt(cv2.max(cv2.blur(gray*gray,(9,9)) - mu*mu, 0))
    h = bgr.shape[0]
    yy = np.arange(h)[:,None]
    shita = (yy < h*0.80)                    # 下2割は空とみなさない

    # ①芯：白い壁(青-赤の差19)と空(28)の間に線を引く。のっぺり判定で窓枠・目地を落とす
    core = (((b-r) > 22) & (lum > 130) & (sd < 9) & shita).astype(np.uint8)*255
    # ②電線ぶんの隙間うめ（21px。これ以上大きくすると壁へ流れ込む）
    grown = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((21,21),np.uint8))
    # ③色が空寄りでない所は捨てる（黒い外壁は明るさ98で落ちる）
    yuru = (((b-r) > 14) & (lum > 110) & shita).astype(np.uint8)*255
    m = cv2.bitwise_and(grown, yuru)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9,9),np.uint8))
    # ④上端からつながっている塊だけ
    n,lab,stats,_ = cv2.connectedComponentsWithStats(m,8)
    top = set(np.unique(lab[0:max(2,int(h*0.02)),:]))
    out = np.zeros_like(m)
    for i in range(1,n):
        if i not in top: continue
        if stats[i,cv2.CC_STAT_AREA] > bgr.shape[0]*bgr.shape[1]*0.02:
            out[lab==i]=255
    return out

def sen_mask(gray, sora):
    """空の中の細い筋。暗い線も明るい線も、太さを変えて3回見る。
       切れ切れに写る電線は、直線として引き直してから消す
       （断片のまま長さで捨てると、ほとんど残ってしまう）"""
    raw = np.zeros_like(gray)
    for k in (7,13,21):
        ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k,k))
        for op in (cv2.MORPH_BLACKHAT, cv2.MORPH_TOPHAT):
            hat = cv2.morphologyEx(gray, op, ker)
            v = hat[sora>0]
            if v.size==0: continue
            th = max(7, float(np.percentile(v,98.6)))
            raw |= (((hat>th) & (sora>0)).astype(np.uint8)*255)
    raw = cv2.morphologyEx(raw, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
    H,W = gray.shape
    lines = cv2.HoughLinesP(raw, 1, np.pi/720, threshold=40,
                            minLineLength=max(40,W//22), maxLineGap=40)
    out = np.zeros_like(raw)
    if lines is not None:
        for x1,y1,x2,y2 in np.asarray(lines).reshape(-1,4):
            dx,dy = float(x2-x1), float(y2-y1)
            n = (dx*dx+dy*dy) ** .5
            if n==0: continue
            ux,uy = dx/n, dy/n
            # 画面いっぱいに伸ばして、その線の上に筋がどれだけ乗っているか数える
            ts = np.arange(-W, W*2, 1.0)
            xs = (x1+ux*ts).astype(int); ys = (y1+uy*ts).astype(int)
            ok = (xs>=0)&(xs<W)&(ys>=0)&(ys<H)
            xs,ys = xs[ok], ys[ok]
            if xs.size < 40: continue
            insky = sora[ys,xs]>0
            if insky.sum() < 40: continue
            hit = (raw[ys,xs]>0) & insky
            if hit.sum() / insky.sum() < 0.50: continue    # 線らしくないものは捨てる
            cv2.line(out,(xs[0],ys[0]),(xs[-1],ys[-1]),255,4)
    # 建物のきわは触らない。空を内側に縮めてから当てる（縮めないと壁や屋根が溶ける）
    safe = cv2.erode(sora, np.ones((21,21),np.uint8))
    out = cv2.bitwise_and(out, safe)
    # 直線に乗らなかった短い筋も、空の中なら消す（アンテナ・支線）
    n,lab,stats,_ = cv2.connectedComponentsWithStats(cv2.dilate(raw,np.ones((3,3),np.uint8)),8)
    for i in range(1,n):
        x,y,w,h,a = stats[i]
        if a>=30 and max(w,h)>=45 and a <= max(w,h)*12:
            tmp=np.zeros_like(out); tmp[lab==i]=255
            out |= cv2.bitwise_and(tmp,safe)
    return cv2.dilate(out, np.ones((3,3),np.uint8))

def keshi(path, outpath=None, check=False):
    bgr = cv2.imread(path)
    if bgr is None: raise SystemExit('読めない: '+path)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    sora = sora_mask(bgr)
    sen  = sen_mask(gray, sora)
    ratio = float((sen>0).mean())*100
    if check or outpath is None:
        print(f'{path}  空 {float((sora>0).mean())*100:5.1f}%  消す線 {ratio:5.2f}%')
        return ratio
    fixed = cv2.inpaint(bgr, sen, 4, cv2.INPAINT_TELEA)
    cv2.imwrite(outpath, fixed, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(f'{path} → {outpath}  消した線 {ratio:.2f}%')
    return ratio

if __name__=='__main__':
    a=[x for x in sys.argv[1:] if not x.startswith('--')]
    keshi(a[0], a[1] if len(a)>1 else None, '--check' in sys.argv)
