#!/bin/bash
#
# Stops all containers that are in the docker-compose.dev.yml file. The
# script will use environment variables from a .env file if it exists.
# Otherwise, it will utilize .env.dist. If none exists the script exits
# with status code 1.

ENV_FILES=('.env' '.env.dist')
DOCKER_FILE='docker-compose.dev.yml'
CURRENT_DIR=$(pwd)

for FILE in "${ENV_FILES[@]}"; do
  if [[ -f $FILE ]]; then
    ENV_FILE="$FILE"
    echo -e "${ENV_FILE} selected as a file with environment variables.\n"
    break
  fi
done

if [[ -z $ENV_FILE ]]; then
  echo "None of " "${ENV_FILES[@]}" " exists in the ${CURRENT_DIR}"
  exit 1
fi

if ! [[ -f $DOCKER_FILE ]]; then
  echo "${FILE} doesn't exist in the ${CURRENT_DIR}."
  exit 1
fi

if docker-compose --env-file="$ENV_FILE" -f "$DOCKER_FILE" down "$@"; then
  echo -e "\033[1;32mSuccess\033[0m"
else
  echo -e "\033[1;31mFailure\033[0m"
fi
