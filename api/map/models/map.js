'use strict';

/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#lifecycle-hooks)
 * to customize this model
 */


async function setSlug(map) {
    // Create slugs for nodes for better Map admin usage

    const nodes = await strapi.query('node').find({_limit:-1});
    
    async function getNodeTitle(id, field='title') {
        if (id) {
            const nodeFound = nodes.filter(node => node.id == id)[0]
            if (nodeFound) {
                return nodeFound[field]
            }
        }
        return null
    }

    if (map.node_mapping){
        await Promise.all(
            map.node_mapping?.map(async nodeMapping => {
                const sourceTitle = await getNodeTitle(nodeMapping.source, 'slug')
                const targetTitle = await getNodeTitle(nodeMapping.target, 'slug')
                nodeMapping.slug = [sourceTitle, targetTitle]
                    .filter(element => element != null)
                    .join(' -> ')
            }))
    }


    return map
}

module.exports = {
    lifecycles: {
        beforeCreate: async (map) => {
            map = await setSlug(map)
        },
        beforeUpdate: async (params, map) => {
            map = await setSlug(map)
        },
    },
};
