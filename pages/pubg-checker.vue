<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-2xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          PUBG Mobile User ID Checker
        </h1>
        <p class="text-lg text-gray-600">
          Check if a PUBG Mobile user ID is valid and get player information
        </p>
      </div>

      <!-- Input Form -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="mb-4">
          <label for="userid" class="block text-sm font-medium text-gray-700 mb-2">
            PUBG Mobile User ID
          </label>
          <input
            id="userid"
            v-model="userid"
            type="text"
            placeholder="Enter user ID (e.g., 5204837417)"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            :disabled="loading"
            @keyup.enter="checkUserID"
          />
        </div>
        
        <button
          @click="checkUserID"
          :disabled="loading || !userid"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <span v-if="loading" class="flex items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Checking...
          </span>
          <span v-else>Check User ID</span>
        </button>
      </div>

      <!-- Results -->
      <div v-if="result" class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">Results</h2>
        
        <!-- Success Result -->
        <div v-if="result.status === 'success'" class="bg-green-50 border border-green-200 rounded-md p-4">
          <div class="flex items-center mb-3">
            <svg class="w-6 h-6 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <span class="text-green-800 font-medium">Valid User ID</span>
          </div>
          
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">User ID:</span>
              <span class="font-medium">{{ result.userid }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Player Name:</span>
              <span class="font-medium">{{ result.player_name }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">OpenID:</span>
              <span class="font-medium">{{ result.openid }}</span>
            </div>
          </div>
        </div>

        <!-- Invalid Result -->
        <div v-else-if="result.status === 'invalid'" class="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <div class="flex items-center mb-3">
            <svg class="w-6 h-6 text-yellow-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
            <span class="text-yellow-800 font-medium">Invalid User ID</span>
          </div>
          
          <div class="flex justify-between">
            <span class="text-gray-600">User ID:</span>
            <span class="font-medium">{{ result.userid }}</span>
          </div>
          <div class="mt-2 text-yellow-700">
            {{ result.error }}
          </div>
        </div>

        <!-- Error Result -->
        <div v-else class="bg-red-50 border border-red-200 rounded-md p-4">
          <div class="flex items-center mb-3">
            <svg class="w-6 h-6 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="text-red-800 font-medium">Error</span>
          </div>
          
          <div class="text-red-700">
            {{ result.error }}
          </div>
        </div>
      </div>

      <!-- Recent Checks -->
      <div v-if="recentChecks.length > 0" class="bg-white rounded-lg shadow-md p-6 mt-6">
        <h2 class="text-xl font-semibold mb-4">Recent Checks</h2>
        <div class="space-y-2">
          <div
            v-for="check in recentChecks"
            :key="check.timestamp"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-md"
          >
            <div class="flex items-center">
              <div
                :class="{
                  'w-3 h-3 rounded-full mr-3': true,
                  'bg-green-500': check.result.status === 'success',
                  'bg-yellow-500': check.result.status === 'invalid',
                  'bg-red-500': check.result.status === 'error'
                }"
              ></div>
              <span class="font-medium">{{ check.userid }}</span>
            </div>
            <div class="text-sm text-gray-500">
              {{ formatTime(check.timestamp) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const userid = ref('')
const loading = ref(false)
const result = ref(null)
const recentChecks = ref([])

const checkUserID = async () => {
  if (!userid.value.trim()) return
  
  loading.value = true
  result.value = null
  
  try {
    const response = await $fetch('/api/check-pubg', {
      method: 'POST',
      body: {
        userid: userid.value.trim()
      }
    })
    
    result.value = response
    
    // Add to recent checks
    recentChecks.value.unshift({
      userid: userid.value.trim(),
      result: response,
      timestamp: Date.now()
    })
    
    // Keep only last 10 checks
    if (recentChecks.value.length > 10) {
      recentChecks.value = recentChecks.value.slice(0, 10)
    }
    
  } catch (error) {
    result.value = {
      status: 'error',
      userid: userid.value.trim(),
      error: error.message || 'Failed to check user ID'
    }
  } finally {
    loading.value = false
  }
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString()
}
</script>

<style scoped>
/* Add any custom styles here */
</style>