#!/bin/bash

BASE_URL=":8000"
UNIQUE_ID=$(date +%s)
USERNAME="user_$UNIQUE_ID"
EMAIL="user_$UNIQUE_ID@example.com"
PASSWORD="password"

echo "1. POST /signup"
echo "Signing up as new user: $USERNAME"
http POST $BASE_URL/signup \
    username=$USERNAME \
    email=$EMAIL \
    password=$PASSWORD \
    password2=$PASSWORD \
    | jq
echo

echo "2. POST /auth/login"
echo "Logging in..."
AUTH_RESPONSE=$(http POST $BASE_URL/auth/login \
    username=$USERNAME \
    password=$PASSWORD)

AUTH_TOKEN=$(echo $AUTH_RESPONSE | jq -r '.token')

if [ "$AUTH_TOKEN" == "null" ] || [ -z "$AUTH_TOKEN" ]; then
    echo "Login failed. Response:"
    echo $AUTH_RESPONSE | jq
    exit 1
fi

echo "Logged in. Authorization token: $AUTH_TOKEN"
echo

echo "3. POST /todos/"
echo "Creating new todo..."
TODO_RESPONSE=$(http POST $BASE_URL/todos/ \
    "Authorization: Token $AUTH_TOKEN" \
    name="new todo" \
    description="new desc")

TODO_ID=$(echo $TODO_RESPONSE | jq -r '.id')
echo "Created Todo ID: $TODO_ID"
echo $TODO_RESPONSE | jq
echo

echo "4. GET /todos/"
echo "Listing todos..."
http GET $BASE_URL/todos/ \
    "Authorization: Token $AUTH_TOKEN" \
    | jq
echo

echo "5. GET /todos/$TODO_ID"
echo "Fetching specific todo..."
http GET $BASE_URL/todos/$TODO_ID \
    "Authorization: Token $AUTH_TOKEN" \
    | jq
echo

echo "6. PUT /todos/$TODO_ID"
echo "Updating todo..."
http PUT $BASE_URL/todos/$TODO_ID \
    "Authorization: Token $AUTH_TOKEN" \
    name="updated todo name" \
    description="updated todo desc" \
    | jq
echo

echo "7. POST /todos/$TODO_ID/items"
echo "Creating todo item..."
http POST $BASE_URL/todos/$TODO_ID/items \
    "Authorization: Token $AUTH_TOKEN" \
    name="test todos" \
    | jq
echo

echo "8. GET /todos/$TODO_ID (Fetching Item ID)"
TODO_WITH_ITEMS=$(http GET $BASE_URL/todos/$TODO_ID \
    "Authorization: Token $AUTH_TOKEN")
ITEM_ID=$(echo $TODO_WITH_ITEMS | jq -r '.items[0].id')

if [ "$ITEM_ID" == "null" ] || [ -z "$ITEM_ID" ]; then
    echo "Failed to retrieve Item ID."
    exit 1
fi

echo "Found Item ID: $ITEM_ID"
echo

echo "9. GET /todos/$TODO_ID/items/$ITEM_ID"
echo "Fetching specific item..."
http GET $BASE_URL/todos/$TODO_ID/items/$ITEM_ID \
    "Authorization: Token $AUTH_TOKEN" \
    | jq
echo

echo "10. PUT /todos/$TODO_ID/items/$ITEM_ID"
echo "Updating item (completing it)..."
http PUT $BASE_URL/todos/$TODO_ID/items/$ITEM_ID \
    "Authorization: Token $AUTH_TOKEN" \
    name="Buy Almond Milk" \
    is_complete=true \
    | jq
echo

echo "11. DELETE /todos/$TODO_ID/items/$ITEM_ID"
echo "Deleting item..."
http DELETE $BASE_URL/todos/$TODO_ID/items/$ITEM_ID \
    "Authorization: Token $AUTH_TOKEN" \
    | jq
echo

echo "12. DELETE /todos/$TODO_ID"
echo "Deleting todo..."
http DELETE $BASE_URL/todos/$TODO_ID \
    "Authorization: Token $AUTH_TOKEN" \
    | jq
echo

echo "13. GET /todos/ (Verify empty)"
http GET $BASE_URL/todos/ \
    "Authorization: Token $AUTH_TOKEN" \
    | jq
echo

echo "14. GET /auth/logout"
echo "Logging out..."
http GET $BASE_URL/auth/logout \
    "Authorization: Token $AUTH_TOKEN" \
    | jq
echo

echo "Tests Completed Successfully."
