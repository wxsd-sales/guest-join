# Guest Join
  
Join a Webex meeting (PMR, SIP address, or Meeting Number) as a Guest, or create a link for a guest to use later.

<!--[![Vidcast Overview](https://github.com/wxsd-sales/custom-pmr-pin/assets/19175490/4861e7cd-7478-49cf-bada-223b30810691)](https://app.vidcast.io/share/3f264756-563a-4294-82f7-193643932fb3)-->


## Overview
Simply enter a name, and a Webex destination and click "Join," or click "Get Link" to save the Guest name and destination as a link to use later.


## Setup

### Prerequisites & Dependencies:

- Developed on MacOS Ventura (13.4.1)
- Developed on Python 3.8.1 & 3.8.3
-   Other OS and Python versions may work but have not been tested
- Redis

<!-- GETTING STARTED -->

### Installation Steps:
1. 
```
pip install aiohttp
pip install python-dotenv
pip install pyjwt
pip install redis
```
2.  Clone this repo, and create a file named ```.env``` in the repo's root directory.
3.  Populate the following environment variables to the .env file:
```
MY_APP_PORT=8080
MY_APP_HOST="https://your.server.com/session"
MY_REDIS_HOST="localhost"
MY_REDIS_PORT=6379

GUEST_APP_ISS=
GUEST_APP_SECRET=

EMBED_URL="https://your-guest-demo-deployment.com/guest"
```
4. Run
```python server.py```
    
    
## Live Demo

<!-- Update your vidcast link -->
<!-- Check out our Vidcast recording, [here](https://app.vidcast.io/share/3f264756-563a-4294-82f7-193643932fb3)! -->

<!-- Keep the following statement -->
*For more demos & PoCs like this, check out our [Webex Labs site](https://collabtoolbox.cisco.com/webex-labs).

## License

All contents are licensed under the MIT license. Please see [license](LICENSE) for details.

## Disclaimer

<!-- Keep the following here -->  
Everything included is for demo and Proof of Concept purposes only. Use of the site is solely at your own risk. This site may contain links to third party content, which we do not warrant, endorse, or assume liability for. These demos are for Cisco Webex usecases, but are not Official Cisco Webex Branded demos.
 
 
## Support

Please contact the Webex SD team at [wxsd@external.cisco.com](mailto:wxsd@external.cisco.com?subject=CustomPMRPIN) for questions. Or for Cisco internal, reach out to us on Webex App via our bot globalexpert@webex.bot & choose "Engagement Type: API/SDK Proof of Concept Integration Development". 
