# Booking monitor

Runs outside the booking backend and outside the owner's computer, every 30 minutes
at UTC minutes 7 and 37. Uses the free standard Linux runner in this public repository;
no paid API, artifacts, caches, or advertising changes.

Read-only HTTP probes check the homepage, booking page, calendar script/styles and
public slots API including JSON shape and CORS. A failed probe gets one retry.
Zero available slots is not itself a failure. No customer details are stored, no
analytics events are sent and no booking is submitted. This cannot prove final
booking submission or detect every browser-specific rendering problem.

GitHub assignment/issue notifications alert the owner on a new incident; subscribed
issue comments notify changes and recovery. Matching repeated failures remain silent.
An open issue authored by github-actions[bot] stores only public endpoint failures;
it closes on recovery. No mailbox credentials or repository secrets are required.
The workflow runs from the default branch or authorized manual dispatch, never PRs.

Manual dispatch with notification_test=true creates one explicitly labelled test
issue assigned to the owner, without fabricating website failure. Close this test
issue after verifying delivery. Infrastructure failures use native workflow failure
notifications, already enabled for the owner. The owner must keep GitHub email
notifications enabled for assignments, participating issues, and workflow failures.

GitHub schedules can be delayed or dropped during service load/outages; 30 minutes
is a target interval, not a guaranteed detection SLA. Public-repository schedules
are disabled after 60 days without repository activity. Keep this schedule's enabled
state and last successful run in the existing weekly website review. If homepage
calendar implementation changes, update the three expected markers in probe().
