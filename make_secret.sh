
file=./.env
if [ -e "$file" ]; then echo "file .env exists"
else echo "making  .env file"
cp .env.example .env
fi
