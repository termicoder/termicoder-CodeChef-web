# termicoder-codechef-web

**THIS IS A WORK IN PROGRESS AND NOT READY FOR USE YET**

**The main working ideas can be found in [termicoder/previous_alpha](https://github.com/termicoder/termicoder/tree/previous_alpha/termicoder/judges/codechef) which provided the functionalities for module based implementation of termicoder**

codechef plugin for termicoder using web api


## NOTE:
The codechef plugin implementation supplied with main termicoder repo uses endpoint `https://api.codechef.com/` for accessing resources.

This judge plugin on contrary uses `https://www.codechef.com/api/` based urls as well as direct access to html and forms using beautiful soup to achive the required termicoder functionalies.

The purpose of creating this is that during a prior contest([LTIME64](https://www.codechef.com/LTIME64)) , codechef disabled access to its oauth based api `https://api.codechef.com` which rendered termicoder useless during the contest. Codechef as of now cannot disable access to `https://www.codechef.com/api` endpoints as they are directly being used in their web interface `www.codechef.com` to get ajax requests and load problems and contests after regular intervals.

This is provided externally as we believe that overtime the codechef web interface will also shift to `https://api.codechef.com` and the endpoints should be more stable. On the other case If codechef shifts to some other paradigm and completely does away with frontend access to the api, we can still emulate complete html based browser functionality to keep this working.

In this instead of saving Oauth tokens, we save coookies after a user logs in. This currently does not support saving of password.

Another reason for using this is that the web api supports submissson but https://api.codechef.com doesn't (yet).
