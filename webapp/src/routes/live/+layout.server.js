export function load() {
  return {
    streams: [
      {
        id: 1,
        channelNames: ['BNSF/UP'],
        url: 'https://broadcastify.cdnstream1.com/8083',
        title: 'BNSF/UP Seattle Sub - North End',
        active: true,
      },
      {
        id: 2,
        channelNames: ["NS", "CSX"],
        url: 'https://broadcastify.cdnstream1.com/6752',
        title: 'Decatur Area CSX and Norfolk Southern Rail',
        active: false,
      }
    ],
    transcriptions: {
      "1": [
        {
          channel: 0,
          text: "So it's FRA tomorrow, so I have a shift motor in the car.",
          time: "2023-12-02T14:21:10.627-08:00",
          speaker: "Dispatcher"
        },
        {
          channel: 0,
          text: "You got a hand out?",
          time: "2023-12-02T14:23:11.627-08:00"
        },
        {
          channel: 0,
          text: "Hello. »» Thank you for calling BNSF Railway. Our menu has changed. For quality or training purposes. »» Can I get my list back? »» You guys take, take, take, and never give. Tell me what. I'm going to take Damien's job now, too. We're likely out. Huh? No. »» Please hold for the next available agent. This is a little bestie friend. He comes in handy. Or, right on the nose, like right on the nose. He loves the nose. It's in there. It's in there. All right, if you're working on the turnover, I'll work on like kind of the chuck part of the middle of the turnover. Please hold for the next available agent.",
          time: "2023-12-02T14:23:32.627-08:00"
        },
        {
          channel: 0,
          text: "All representatives are busy. To leave a voicemail, press 1. »» Go ahead there, mister. »» Oh, yeah. »» See you. »» That's tactical, Mason. »» That's tactical, Mason. »» Tacoma, you heard him. »» Hey, I hate to say this, Kevin, but your radio is stuck, but we're going to work on 14.",
          time: "2023-12-02T14:24:25.627-08:00"
        },
        {
          channel: 0,
          text: "What channel did you say you're going to there, J.D.? »» Channel 14. »» I'll do that. »» Ok, did you tell Blake we're going to need that light at River Street to come out? »» I did. And I told him you probably need a poke, you might need a poke off the old truck lead, but I wasn't sure. »» Ok. »» You should be setting it up. I told him we need it once for the work train and once for you. »» Oh, thanks. Ok, thanks, Kevin.",
          time: "2023-12-02T14:25:32.627-08:00"
        },
        {
          channel: 0,
          text: "Four cars. »» Four now.",
          time: "2023-12-02T14:25:41.627-08:00"
        },
        {
          channel: 0,
          text: "Contact 41.",
          time: "2023-12-02T14:26:05.627-08:00"
        },
        {
          channel: 0,
          text: "And on mark.",
          time: "2023-12-02T14:26:21.627-08:00"
        }
      ].reduce((acc, { channel, text, time }) => {
        // TODO: move this to backend
        const components = text.split("»»").map(speakerText => ({
          text: speakerText.trim(),
          time,
          channel,
        }));
        
        return [...acc, ...components];
      }, []),
    }
  };
}
