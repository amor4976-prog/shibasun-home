# Booking monitor

Runs outside the booking backend and outside the owner's computer, every 30 minutes
at UTC minutes 7 and 37. Uses the free standard Linux runner in this public repository;
no paid API, artifacts, caches, or advertising changes.

Read-only HTTP probes check the homepage, booking page, calendar script/styles and
public slots API including JSON shape and CORS. A failed probe gets one retry.
Zero available slots is not itself a failure. No customer details are stored, no
analytics events are sent and no booking is submitted. This cannot prove final
booking submission or detect every browser-specific rendering problem.

An email is sent to the owner on failure, changed failure, and recovery. Matching
repeated failures remain silent. An open issue authored by github-actions[bot]
stores only the public endpoint failure signature; it is closed on recovery.
SMTP credentials live only in encrypted repository secrets; never put them in files.
The workflow runs only from the default branch or an authorized manual dispatch,
not from pull requests. Keep repository write access restricted to trusted users.

Manual dispatch with notification_test=true sends one explicitly labelled test
email without fabricating a website failure or altering the real incident state.
Monitor infrastructure failures trigger a separate warning email.

GitHub schedules can be delayed or dropped during service load/outages; 30 minutes
is a target interval, not a guaranteed detection SLA. Public-repository schedules
are disabled after 60 days without repository activity. Keep this schedule's enabled
state and last successful run in the existing weekly website review. If homepage
calendar implementation changes, update the three expected markers in probe().
