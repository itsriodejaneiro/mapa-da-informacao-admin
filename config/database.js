module.exports = ({ env }) => ({
  defaultConnection: 'default',
  connections: {
    default: {
      connector: 'mongoose',
      settings: {
        "uri": env('URI')
      },
      options: {
        ssl: true,
      },
    },
  },
});
