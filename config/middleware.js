module.exports = ({ env }) => ({
    settings: {
        cache: {
            enabled: true,
            // type: 'redis',
            models: [
                {
                    model: 'map',
                    hitpass: false
                }
            ],
            // redisConfig: {
            //     uri: process.env.REDIS_URL
            // },
        }

    }
});