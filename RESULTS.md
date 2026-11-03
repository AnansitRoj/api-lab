# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: The Rough Americana
- Step 0.12, results of the three runs without a session (optional): skipped
- Step 0.16, blocks of "how many of the three tools are excluded": 0 tools excluded, 1 tool excluded, 2 tools excluded, 3 tools excluded (all). The first test used only the block "1 tool". I added the inputs [], ["Knife", "Scissors"] and all three tools ["Knife", "Pizza cutter", "Scissors"]. Only the block "all three tools" failed, and it revealed the defect.

## Defect report
- Title: Excluding all three tools makes POST /api/pizza answer 500 with an empty body
- Request: POST https://quickpizza.grafana.com/api/pizza with header Authorization: token <token of a logged-in user> and body {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
- Expected result: status 400 and a JSON error message, because no pizza can satisfy the request
- Actual result: status 500 Internal Server Error and an empty body (Content-Length: 0), confirmed with curl and with pytest (assert 500 == 200)
- Severity: Medium. A customer input makes the server fail, and the app gets no message to show the customer.

## Part A
- Step A4, status codes when the other user reads, changes and deletes:

## Part B
1.
2.
3.
4.
5.
6.
7.
8.