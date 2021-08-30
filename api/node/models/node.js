'use strict';

/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#lifecycle-hooks)
 * to customize this model
 */


async function setSlug(node) {

    node.slug = [node.title, node.subtitle]
        .filter(element => element && element.length) // filter out null fields
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
