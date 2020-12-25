freeze:
	pip freeze | grep -v "pkg-resources" > req.txt
