if [ -z "$OPENAI_API_KEY" ]; then
    export OPENAI_API_KEY=$(echo 'c2stcHJvaj...' | base64 -d)
fi

python run.py