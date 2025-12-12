<template>
  <nav class="bg-gradient-to-r from-emerald-600 to-emerald-700 text-white shadow-lg">
    <div class="max-w-7xl mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        <router-link to="/" class="flex items-center gap-3 hover:opacity-90 transition">
          <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
          </svg>
          <div>
            <h1 class="text-xl font-bold">Sound City</h1>
            <p class="text-xs text-emerald-100">Münster Livability Index</p>
          </div>
        </router-link>

        <div class="flex items-center gap-6">
          <router-link
            to="/"
            class="hover:text-emerald-200 transition font-medium"
            active-class="text-white border-b-2 border-white"
          >
            Map
          </router-link>
          <router-link
            to="/about"
            class="hover:text-emerald-200 transition font-medium"
            active-class="text-white border-b-2 border-white"
          >
            About
          </router-link>
          <a
            href="https://github.com/Geoinformation-in-Society/SoundCity"
            target="_blank"
            class="hover:text-emerald-200 transition font-medium"
          >
            GitHub
          </a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>