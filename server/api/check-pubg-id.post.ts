export default defineEventHandler(async (event) => {
  const { userid } = await readBody(event)
  
  if (!userid) {
    throw createError({
      statusCode: 400,
      statusMessage: 'User ID is required'
    })
  }

  try {
    const response = await $fetch('https://api.elitedias.com/checkid', {
      method: 'POST',
      headers: {
        'origin': 'https://elitedias.com',
        'referer': 'https://elitedias.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36',
        'Content-Type': 'application/json'
      },
      body: {
        game: 'pubgm',
        userid: userid
      }
    })

    if (response.valid === 'valid') {
      return {
        status: 'valid',
        pubg_name: response.name || 'NA'
      }
    } else {
      return {
        status: 'invalid',
        error: 'UserID is not valid'
      }
    }
  } catch (error) {
    return {
      status: 'error',
      error: `Request failed: ${error.message}`
    }
  }
})