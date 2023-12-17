export function load() {
  return {
    streams: [
      {
        id: 1,
        url: 'https://broadcastify.cdnstream1.com/8083',
        webpage: 'https://www.broadcastify.com/listen/feed/8083',
        title: 'BNSF/UP Seattle Sub - North End',
        channels: 1,
      },
      {
        id: 2,
        url: 'https://broadcastify.cdnstream1.com/6752',
        webpage: 'https://www.broadcastify.com/listen/feed/6752',
        title: 'Decatur Area CSX and Norfolk Southern Rail',
        channels: 2,
      }
    ]
  };
}
