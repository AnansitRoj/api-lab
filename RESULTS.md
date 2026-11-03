# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: The Rough Americana
- Step 0.12, results of the three runs without a session (optional): skipped
- Step 0.16, blocks of "how many of the three tools are excluded": 0 tools excluded, 1 tool excluded, 2 tools excluded, 3 tools excluded (all). The first test used only the block "1 tool". I added the inputs [], ["Knife", "Scissors"] and all three tools ["Knife", "Pizza cutter", "Scissors"]. Only the block "all three tools" failed, and it revealed the defect.

## Defect report

### Defect 1
- Title: Excluding all three tools makes POST /api/pizza answer 500 with an empty body
- Request: POST https://quickpizza.grafana.com/api/pizza with header Authorization: token <token of a logged-in user> and body {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
- Expected result: status 400 and a JSON error message, because no pizza can satisfy the request
- Actual result: status 500 Internal Server Error and an empty body (Content-Length: 0), confirmed with curl and with pytest (assert 500 == 200)
- Severity: Medium. A customer input makes the server fail, and the app gets no message to show the customer.

### Defect 2
- Title: GET /api/ratings accepts a made-up token and returns the ratings
- Request: GET https://quickpizza.grafana.com/api/ratings with the header Authorization: token 0000000000000000 (a made-up token of 16 characters that no login ever gave out)
- Expected result: status 401 and {"error": "authentication failed"}, as for a request without a token
- Actual result: status 200 and a list of 50 ratings (ids 1 to 132). In Step A2 a token of 3 characters was refused with 401, so the server seems to check only the form of the token and not whether it belongs to a user.
- Severity: High. A stranger can read data without an account.

## Part A
- Step A4, status codes when the other user reads, changes and deletes: read = 404, update = 400, delete = 400

## Part B
1. Two kinds of failure that tests against a real server can find and a unit test with stubs cannot: (a) a problem in how the servers are set up, for example a load balancer that sends a request to a server that does not know the new user, so the login fails; (b) a fault in how the real parts work together, for example the server answering 500 with an empty body for a request that the code behind it cannot handle, which I found in Step 0.16. A reason to write unit tests with stubs as well: they run fast without a network, give the same result every time, and point to the faulty function directly.
2. The public token belongs to everyone, so another student could change my ratings while my test runs and the result would be wrong. Each test therefore creates its own user with a new random name, logs in, and uses its own token, so no test can disturb another and I never change data that is not mine. In Project 2, each test will create its own data in the shared shop or hotel (for example a cart or a booking) with names that nobody else uses, will change and delete only what it created, and will never touch the data of other groups.
3. A session keeps the cookies that the site sends back. QuickPizza runs on several servers behind a load balancer, and each server keeps its own users. The AWSALB cookie tells the load balancer to send all my requests to the same server. If every request is sent on its own without the cookie, the login may reach a server that has never seen the new user and fail with 401, so the test passes on some runs and fails on others (a flaky test). I skipped Step 0.12, so I have no results of my own for the runs without a session.
4. The block "all three tools excluded" revealed the defect, and the other blocks passed. A 500 with an empty body is worse for an app than a 400 with a message, because the app has no text to show the customer and cannot tell whether the input was wrong or the server broke, while a 400 with a message says that the request must be changed. The test stays in the suite as xfail instead of being deleted so that the defect stays in view while the rest of the suite is green, and because of strict=True the run fails as soon as QuickPizza fixes the defect, which tells me to remove the mark.
5. Base choice coverage needs 1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9 tests: one base test, then one test for each non-base block of each characteristic. All combinations coverage would need 3 x 4 x 2 x 3 = 72 tests.
6. The other user got 404 when reading the rating, 400 when changing it and 400 when deleting it. I expected a code from 400 to 499 for each attempt, for example 403 Forbidden or 404 Not Found, and that is what happened, because every attempt was refused and the owner's rating did not change. The codes are not exact: 400 normally means that the request itself is malformed, while 403 would say that the user has no permission, and read (404) and change or delete (400) are not consistent with each other. I do not treat this as a defect, because nobody could read, change or delete the rating of another user. It is a small problem with how clear the status codes are, and I did not check the error messages.
7. The command with the made-up token 0000000000000000 returned status 200 and a list of 50 ratings, not 401. This is a defect (Defect 2 above), because the token never came from a login, yet the server served the data. It seems that the server checks only the form of the token, since a token of 3 characters was refused with 401 in Step A2, but I did not test this further. On a real system a stranger could read the data of other users without an account. With a write operation, which I did not try, a stranger could create, change or delete data, or act as another user, and a token that is easy to guess makes it worse.
8. An API test checks the data and the status codes better than a test through the web pages: it is faster, it can check every field of a JSON answer and every error message exactly, and it can send inputs that the web form would never allow, such as 0 or 6 stars. Only a test through the web pages can check what the user sees on the screen, for example a button in the wrong place, a text that is cut off, or a page that looks broken.