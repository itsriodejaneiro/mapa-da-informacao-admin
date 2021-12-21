'use strict';
const { sanitizeEntity } = require('strapi-utils');


/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#core-controllers)
 * to customize this controller
 */

function split_context(_map) {
  return _map.node_mapping.forEach(element => {
    if (element.context && element.context.length > 0){
      let context = element.context.split(',')
      context = context.map(item => item.trim())
      element.context = context
    }
  });
}

function populate_context(_map){
  console.log('populate_context', _map.node_mapping.length)

  // populate category.nodes with context from node_mapping 
  _map.node_mapping.forEach(element => {
    let source = element.source
    let target = element.target
    let context = element.context

    if (context && context.length > 0){
      // console.log('context', context)
      // for each category
      _map.categories.forEach(category => {
        
        // console.log('source', source._id, 'target', target._id)
        // console.log(category.nodes.map(node => node._id))
        // find respective nodes
        category.nodes.forEach(node => {
          if (String(node._id) == String(source._id) || String(node._id) == String(target._id)){
            // populate
            let node_context = node.context
            if (node_context == undefined) 
              node_context = []

            // node.context = [...node_context, ...context]
            node.context = [...new Set([...node_context, ...context])]
          }
        })
      })
    }
  })
}

module.exports = {

  async find(ctx) {
    let entities
    if (ctx.query._q) {
      entities = await strapi.services.map.search(ctx.query)
    } else {
      entities = await strapi.services.map.find(ctx.query)
    }

    entities.map(map => {
      split_context(map)
      populate_context(map)
    })
    return entities.map(entity => sanitizeEntity(entity, { model: strapi.models.map }))
  },

  async findOne(ctx) {
    const { id } = ctx.params
    let entity = await strapi.services.map.findOne({ id })
    entity = sanitizeEntity(entity, { model: strapi.models.map })
    split_context(entity)
    populate_context(entity)
    return entity
  },

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
