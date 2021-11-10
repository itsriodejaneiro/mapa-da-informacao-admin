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

    // return only id and title, omitting other info as it requires password 
    return entities.map(map => {
      return {
        '_id': map._id,
        'id': map.id,
        'title': map.title
      }
    })
    
  },

  async draft(ctx) {
    const { id } = ctx.params;

    const password = ctx.query['password']


    let entities = await strapi.query('map').model.find();

    // find by id, a map that has a password and match password
    const entity = entities.filter(map => map.id == id && map.draft_password && map.draft_password == password)[0]

    return sanitizeEntity(entity, { model: strapi.models.map });
  },
};
