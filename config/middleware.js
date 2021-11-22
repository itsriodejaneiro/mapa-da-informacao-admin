module.exports = ({ env }) => ({
    settings: {
        cache: {
            enabled: true,
            type: 'redis',
            models: [
                {
                    model: 'map',
                    hitpass: false
                }
            ],
            redisConfig: {
                uri: env('CACHING_URL', '127.0.0.1:6379') // default is local redis
            },
        }

    }
});