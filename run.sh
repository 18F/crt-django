#!/bin/bash
# used by local docker container

# # make sure migrations are applied
echo Migrating database...
python /code/crt_portal/manage.py migrate

echo Generating css...
node node_modules/gulp/bin/gulp build-sass

# If LOCALSTACK is set in environment, this will upload static files to the localstack s3 service running in docker
# Otherwise the development server is handling static files
if [[ -n "${USE_LOCALSTACK}" ]]; then
    aws --endpoint-url=${LOCALSTACK_URL} s3 mb s3://crt-portal
    aws --endpoint-url=${LOCALSTACK_URL} s3 mb s3://crt-private
    
    echo Collecting and uploading static assets to localstack...
    python /code/crt_portal/manage.py collectstatic --noinput
else
    # Since the dev server is handling static files, let's rebuild them as we modify
    echo Watching-sass to rebuild as we make changes...
    node node_modules/gulp/bin/gulp watch-sass &
fi;

echo Compiling i8n files…
python /code/crt_portal/manage.py compilemessages

echo Starting Django Server…
python /code/crt_portal/manage.py runserver 0.0.0.0:8000
