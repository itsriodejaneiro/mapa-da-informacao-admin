module.exports = ({ env }) => ({
    settings: {
        cache: {
            enabled: false,
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