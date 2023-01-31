# CREATE FILE requirements.txt: pip freeze > requirements.txt
# CREATE IMAGE: docker build -t get-stoks-by-filter -f Dockerfile.df .
# RUN IMAGE: docker run -p 9000:8080 -d get-stoks-by-filter
# CALL: curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d {}