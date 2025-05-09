#!/usr/bin/env sh

set -e


BASE_URL=$PWD/backend

echo "Dir: $BASE_URL"

cd $BASE_URL

if [ ! -d "node_modules" ]; then
  echo "node_modules folder not found. Running npm install..."
  npm install
fi

npx @tailwindcss/cli -w -i input.css -o "$BASE_URL/pointsheet/static/style.css"
