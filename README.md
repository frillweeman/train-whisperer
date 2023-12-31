# Train Whisperer [[Live Site](https://youthfulgoon.com)]

Train Whisperer allows people to listen to and transcribe live railroad radio streams. Any stream can be added via a Broadcastify URL. This allows users to quickly catch up on what was said over the radio without having to listen to it constantly.

Although this project started as a way for me to listen to train radio, it works with any Shoutcast stream, not limited to trains or even [Broadcastify](https://www.broadcastify.com).

## Stack

### Svelte/SvelteKit
Frontend and partial backend. I wanted to learn Svelte since it's one of the newest UI frameworks and supports SSR, and so far, I like it, despite its immaturity. The FE component of SvelteKit serves the frontend UI. The BE component handles all the business logic of the web app, from MongoDB transactions to RabbitMQ consumption of real-time incoming transcriptions. I tried to find intelligent ways to use Svelte's store model to be more like Vue in that client/component code calls an "action", which updates the store from an API endpoint, or in some cases in my app, an SSE stream.

### Python
The Shoutcast monitor component of this app is written in Python because of the great library support for audio manipulation (e.g. `pydub`) and tolerance toward the unconventional `icy` headers on Shoutcast strams. It holds a connection to a specified Shoutcast server, forms audio segments when a software squelch is broken, and sends them over to OpenAI's [Whisper API](https://openai.com/research/whisper) to be transcribed. From here, it forwards the transcribed audio to RabbitMQ, my message broker of choice, to be consumed by the web app. It also stores the transcriptions in MongoDB for persistence.

### TypeScript
I use TypeScript as much as possible on the Svelte side of things because Javascript is a nightmare to debug. I still use JavaScript where it's required, but if I have a choice between JS and TS, it's TS all the way.

### MongoDB
I decided on Mongo since it's a NoSQL db, and I do not have any or anticipate any complex schemas for this app.

### Docker / Docker Compose
Each service (web app, Shoutcast monitor, MongoDB, RabbitMQ) is containerized and connected via `docker-compose`. I initially wanted to make a few distributed microservices on AWS native infrastructure, but the limiting factor was the cost of streaming audio all day. I settled on a DigitalOcean droplet for a few bucks a month that has the resources to run the containers without costing a fortune.
