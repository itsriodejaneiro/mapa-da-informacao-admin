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
                host: env('REDIS_HOST', '127.0.0.1'),
                port: env('REDIS_PORT', 6379),
                password: env('REDIS_PASSWORD', null)
            },
        }

    }
});