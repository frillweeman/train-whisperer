<script>
  export let data;

  $: activeStream = data.streams.find(stream => stream.active);
</script>

<div>
  {#if activeStream}
    <!-- redirect -->
  {:else}
    <div>No fucking active streams</div>
  {/if}
</div>
