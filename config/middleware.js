module.exports = ({ env }) => ({
    settings: {
        cache: {
            enabled: true,
            type: 'redis',
            cacheTimeout: 400,
            enableEtagSupport: true,
            logs:true,
            models: [
                {
                    model: 'map',
                    hitpass: false
                }
            ],
            redisConfig: {
                uri: env('REDIS_URL', '127.0.0.1:6379') // default is local redis
            },
        }

    }
});