const fetch = require('node-fetch')
const { schedule } = require('@netlify/functions')

const handler = async function() {
  console.log('Automated build triggered.')

  await fetch('', {
    method: 'POST'
  }).then((response) => {
    console.log('Build hook response:', response.json())
  })

  return {
    statusCode: 200
  }
}

module.exports.handler = schedule('0 0 * * 1,3,5', handler)
