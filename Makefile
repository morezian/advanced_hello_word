freeze:
	pip3 freeze | grep -v "pkg-resources" > req.txt
