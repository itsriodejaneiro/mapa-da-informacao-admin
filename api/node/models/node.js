'use strict';

/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#lifecycle-hooks)
 * to customize this model
 */


async function setSlug(node) {


    async function getCategoryTitle(id) {
        if (id) {
            const category = await strapi.services.category.findOne({ 'id': id })
            if (category) {
                return category.title
            }
        }
        return null
    }

    node.slug = [await getCategoryTitle(node.category), node.title]
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
