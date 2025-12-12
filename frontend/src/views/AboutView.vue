<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="max-w-4xl mx-auto px-8">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-800 mb-4">About Sound City</h1>
        <p class="text-xl text-gray-600">
          Making Münster's environmental data accessible and actionable
        </p>
      </div>

      <!-- Mission Section -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">🎯 Our Mission</h2>
        <p class="text-gray-700 leading-relaxed mb-4">
          Sound City is a data visualization platform designed to help residents of Münster
          make informed decisions about where to live based on environmental factors. We combine
          air quality and noise pollution data to create a comprehensive livability index for
          different neighborhoods.
        </p>
        <p class="text-gray-700 leading-relaxed">
          Whether you're moving to Münster or looking for a new place within the city, our
          interactive map and detailed neighborhood profiles help you find areas that match
          your environmental preferences.
        </p>
      </div>

      <!-- How It Works -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">🔍 How It Works</h2>
        <div class="space-y-4">
          <div class="flex gap-4">
            <div class="flex-shrink-0 w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600 font-bold text-xl">
              1
            </div>
            <div>
              <h3 class="font-semibold text-gray-800 mb-1">Data Collection</h3>
              <p class="text-gray-600">
                We gather air quality data from OpenAQ and estimate noise levels based on
                traffic patterns and urban density.
              </p>
            </div>
          </div>

          <div class="flex gap-4">
            <div class="flex-shrink-0 w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600 font-bold text-xl">
              2
            </div>
            <div>
              <h3 class="font-semibold text-gray-800 mb-1">Score Calculation</h3>
              <p class="text-gray-600">
                Each neighborhood receives scores for air quality and noise levels (1-5 scale).
                These are combined into an overall livability score (0-10).
              </p>
            </div>
          </div>

          <div class="flex gap-4">
            <div class="flex-shrink-0 w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600 font-bold text-xl">
              3
            </div>
            <div>
              <h3 class="font-semibold text-gray-800 mb-1">Personalization</h3>
              <p class="text-gray-600">
                Adjust the weights to prioritize what matters most to you. Care more about
                quiet environments? Increase the noise weight!
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Sources -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">📊 Data Sources</h2>
        <div class="space-y-4">
          <div>
            <h3 class="font-semibold text-gray-700 mb-2">Air Quality</h3>
            <ul class="list-disc list-inside text-gray-600 space-y-1">
              <li>OpenAQ - Global air quality data platform</li>
              <li>European Environment Agency (EEA)</li>
              <li>German Federal Environment Agency (Umweltbundesamt)</li>
            </ul>
          </div>
          <div>
            <h3 class="font-semibold text-gray-700 mb-2">Noise Pollution</h3>
            <ul class="list-disc list-inside text-gray-600 space-y-1">
              <li>EU Environmental Noise Directive data</li>
              <li>OpenStreetMap road network analysis</li>
              <li>Traffic density estimates</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Technology -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">⚙️ Technology</h2>
        <p class="text-gray-700 mb-4">Built with modern web technologies:</p>
        <div class="grid grid-cols-2 gap-4">
          <div class="flex items-center gap-2">
            <span class="text-2xl">🐍</span>
            <span class="text-gray-700">FastAPI Backend</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-2xl">💚</span>
            <span class="text-gray-700">Vue.js Frontend</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-2xl">🗺️</span>
            <span class="text-gray-700">Leaflet.js Maps</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-2xl">🎨</span>
            <span class="text-gray-700">Tailwind CSS</span>
          </div>
        </div>
      </div>

      <!-- Team/Contact -->
      <div class="bg-gradient-to-r from-emerald-600 to-emerald-700 rounded-2xl shadow-lg p-8 text-white text-center">
        <h2 class="text-2xl font-bold mb-4">📧 Get in Touch</h2>
        <p class="mb-4">
          Have questions, suggestions, or found an issue? We'd love to hear from you!
        </p>
        <div class="flex justify-center gap-4">
          <a
            href="https://github.com/Geoinformation-in-Society/SoundCity"
            target="_blank"
            class="bg-white text-emerald-600 px-6 py-3 rounded-lg font-medium hover:bg-emerald-50 transition"
          >
            GitHub
          </a>
          <a
            href="mailto:your-email@example.com"
            class="bg-emerald-800 text-white px-6 py-3 rounded-lg font-medium hover:bg-emerald-900 transition"
          >
            Email Us
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// No additional logic needed
</script>