<script>
  import FeedSelection from './FeedSelection.svelte';
  // import DarkMode from './DarkMode.svelte';

  export let data;
</script>

<ul class="mx-auto px-4" style="max-width: 40rem">
  <li class="my-4">
    <FeedSelection streams={data.streams} />
  </li>
  <!-- <li class="my-4">
    <DarkMode />
  </li> -->
</ul>
