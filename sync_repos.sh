for NAME in $(gh repo list 23W-INCO --json name | jq -r '.[] | .name'); do gh repo sync "23W-INCO/$NAME";done;
