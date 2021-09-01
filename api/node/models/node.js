'use strict';

/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#lifecycle-hooks)
 * to customize this model
 */


async function setSlug(node) {

    node.slug = [node.namespace, node.label, node.index]
        // filter out null fields and empty strings
        .filter(element => element != null && (typeof (element) == "string" ? element.length : true)) 
        .join(' - ')

    return node

}
module.exports = {

    lifecycles: {
        beforeCreate: async (node) => {
            node = await setSlug(node)
        },
        beforeUpdate: async (params, node) => {
            node = await setSlug(node)
        },
    },
};
