onghub
======

onghub runs code when you push to GitHub.


::

  $ cat onghub.yml
  secret: "foo"
  root_url: "http://127.0.0.1:8000"

  $ onghub trigger emulbreh/onghub

  $ onghub hook emulbreh/onghub
  http://127.0.0.1:8000/hooks/emulbreh/onghub.2FBJssl9gsafJF3hjapww9DIDoA
  
