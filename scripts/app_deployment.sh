#exits program immediately if a command is not sucessful
set -e

if [ -z "$1" ]; then
    echo "Missing commit message arguement 1"
    exit 1
fi


git add -A

git commit -m "$1"


export PROJECT_NAME="tvratings"
export BUCKET_NAME="${PROJECT_NAME}-app-artifacts"
export DEPLOYMENT_PACKAGE="${PROJECT_NAME}_deployment_package.zip"
export FUNCTION_NAME="${PROJECT_NAME}-alexa-skill"


source avenv/bin/activate

secret_scan_results=$(detect-secrets scan | \
python3 -c "import sys, json; print(json.load(sys.stdin)['results'])" )

# static scan for security credentials that terminates if any secrets are found
if [ "${secret_scan_results}" != "{}" ]; then
    echo "detect-secrets scan failed"
    exit 125
fi

python -m unittest

# removes the deployment .zip package locally if it exists
if [ -e $DEPLOYMENT_PACKAGE ]; then
    rm $DEPLOYMENT_PACKAGE
fi

zip $DEPLOYMENT_PACKAGE -r tvratings externals  \
    -x *__pycache__*  --quiet


#add tvratings_skill.py to root of project
zip -u $DEPLOYMENT_PACKAGE -j handlers/tvratings_skill.py  \
    -x *__pycache__* --quiet

aws s3api put-object --bucket $BUCKET_NAME \
    --key $DEPLOYMENT_PACKAGE \
    --body $DEPLOYMENT_PACKAGE \
    --tagging "cloudformation_managed=no&project=${PROJECT_NAME}&prod=yes"


aws lambda update-function-code --function-name $FUNCTION_NAME \
    --s3-bucket $BUCKET_NAME \
    --s3-key $DEPLOYMENT_PACKAGE \
    --no-cli-pager

deactivate

git push origin dev

echo "pushed to remote"

gh pr create --title "$1" \
--body "Automated PR creation" \
--head dev \
--base master

echo "created PR"

echo "----------------------"
echo "deployment successful"