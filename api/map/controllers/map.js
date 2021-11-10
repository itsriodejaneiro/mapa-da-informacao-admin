'use strict';
const { sanitizeEntity } = require('strapi-utils');


/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#core-controllers)
 * to customize this controller
 */

module.exports = {
  async drafts(ctx) {
    let entities = await strapi.query('map').model.find();

    // filter out published ones
    entities = entities.filter(map => map.published_at == null)

    return entities.map(entity => sanitizeEntity(entity, { model: strapi.models.map }));
  },

  async draft(ctx) {
    const { id } = ctx.params;

    let entities = await strapi.query('map').model.find();

    const entity = entities.filter(map => map.id == id)[0]

    return sanitizeEntity(entity, { model: strapi.models.map });
  },
};
