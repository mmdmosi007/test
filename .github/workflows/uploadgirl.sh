#!/bin/bash

set -e

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "❌ File not found: $FILE"
  exit 1
fi

echo "📦 Uploading: $FILE"
FILE_NAME=$(basename "$FILE")
FILE_SIZE=$(stat -c%s "$FILE")

echo "➡️ Step 1: Start upload"
START_RES=$(curl -s -X POST "https://uploadgirl.ir/api/public-upload/start" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"$FILE_NAME\",\"size\":$FILE_SIZE}")

UPLOAD_ID=$(echo "$START_RES" | sed -n 's/.*"uploadId":"\([^"]*\)".*/\1/p')
OBJECT_KEY=$(echo "$START_RES" | sed -n 's/.*"objectKey":"\([^"]*\)".*/\1/p')

echo "   uploadId: $UPLOAD_ID"
echo "   objectKey: $OBJECT_KEY"

if [ -z "$UPLOAD_ID" ] || [ -z "$OBJECT_KEY" ]; then
  echo "❌ Failed to start upload"
  echo "$START_RES"
  exit 1
fi

echo "➡️ Step 2: Get presigned URL"
PART_RES=$(curl -s "https://uploadgirl.ir/api/public-upload/part-url?uploadId=$UPLOAD_ID&objectKey=$OBJECT_KEY&partNumber=1")

PRESIGNED_URL=$(echo "$PART_RES" | sed -n 's/.*"url":"\([^"]*\)".*/\1/p' | sed 's/\\u0026/\&/g')

echo "   URL received"

if [[ "$PRESIGNED_URL" == "" ]]; then
  echo "❌ Failed to get pre-signed URL"
  echo "$PART_RES"
  exit 1
fi

echo "➡️ Step 3: Upload file"
curl -X PUT "$PRESIGNED_URL" --upload-file "$FILE" --silent --show-error

echo "➡️ Step 4: Complete upload"
COMPLETE_RES=$(curl -s -X POST "https://uploadgirl.ir/api/public-upload/complete" \
  -H "Content-Type: application/json" \
  -d "{\"uploadId\":\"$UPLOAD_ID\",\"objectKey\":\"$OBJECT_KEY\",\"parts\":[{\"PartNumber\":1}]}")

FINAL_CODE=$(echo "$COMPLETE_RES" | sed -n 's/.*"code":"\([^"]*\)".*/\1/p')

echo ""
echo "🎉 Uploaded successfully!"
echo "🔗 Final URL:"
echo "https://uploadgirl.ir/d/$FINAL_CODE"
