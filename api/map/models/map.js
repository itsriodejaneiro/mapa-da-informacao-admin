'use strict';

/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#lifecycle-hooks)
 * to customize this model
 */


async function setSlug(map) {
    // Create slugs for nodes for better Map admin usage

    async function getNodeTitle(id) {
        if (id) {
            const nodeFound = await strapi.services.node.findOne({ 'id': id })
            if (nodeFound) {
                return nodeFound.title
            }
        }
        return null
    }


    await Promise.all(
        map.node_groups.map(async node => {

            const currentNode = await getNodeTitle(node.node)
            let nextNodes = []

            // get all nodes names and concat
            if (node.next_nodes){
                for (let nextNode of node.next_nodes) {
                    const nodeTitle = await getNodeTitle(nextNode)
                    if (nodeTitle) {
                        nextNodes.push(nodeTitle)
                    }
                }
            }
            const nextNode = nextNodes.join(', ')

            node.slug = [currentNode, nextNode]
                .filter(element => element && element.length) // filter out null fields
                .join(': ')
        })
    )
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
