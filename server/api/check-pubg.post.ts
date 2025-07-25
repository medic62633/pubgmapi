import { spawn } from 'child_process'
import { defineEventHandler, readBody, createError } from 'h3'

export default defineEventHandler(async (event) => {
  try {
    const body = await readBody(event)
    const { userid } = body

    if (!userid) {
      throw createError({
        statusCode: 400,
        statusMessage: 'User ID is required'
      })
    }

    // Call the Python script with the user ID as command line argument
    return new Promise((resolve, reject) => {
      const pythonProcess = spawn('python', ['pubg_checker_api.py', userid], {
        stdio: ['pipe', 'pipe', 'pipe']
      })

      let output = ''
      let errorOutput = ''

      // Collect output
      pythonProcess.stdout.on('data', (data) => {
        output += data.toString()
      })

      pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString()
      })

      pythonProcess.on('close', (code) => {
        if (code === 0 || code === null) {
          try {
            // Parse the JSON output from Python
            const result = JSON.parse(output.trim())
            resolve(result)
          } catch (parseError) {
            resolve({
              status: 'error',
              userid: userid,
              error: 'Failed to parse Python output',
              raw_output: output
            })
          }
        } else {
          reject(createError({
            statusCode: 500,
            statusMessage: 'Python script execution failed',
            data: {
              error: errorOutput,
              code: code
            }
          }))
        }
      })

      pythonProcess.on('error', (error) => {
        reject(createError({
          statusCode: 500,
          statusMessage: 'Failed to start Python process',
          data: { error: error.message }
        }))
      })

      // Set a timeout
      setTimeout(() => {
        pythonProcess.kill()
        reject(createError({
          statusCode: 500,
          statusMessage: 'Python script timeout'
        }))
      }, 30000) // 30 second timeout
    })

  } catch (error) {
    throw createError({
      statusCode: 500,
      statusMessage: 'Internal server error',
      data: { error: error.message }
    })
  }
}) 