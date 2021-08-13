'use strict';

/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#core-controllers)
 * to customize this controller
 */
 async function find(ctx) {
    let nodes;
        nodes = await strapi.services.node.find();

        const next_node_ids = []

        if (nodes && nodes.length) {
            nodes.forEach((node) => {
                if (node.updated_by) {
                    delete node.updated_by
                }
                if (node.created_by) {
                    delete node.created_by
                }

                if (node && node.next_nodes && node.next_nodes.length) {
                    const next_node_list = node.next_nodes
                    const next_node_ids = []
                    next_node_list.forEach((nextNode) => {
                        next_node_ids.push(nextNode.id)
                    })
                    node.next_nodes = next_node_ids
                }
            })
        }

        return nodes
}

module.exports = {
    find
};
