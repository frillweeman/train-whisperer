<script>
  export let data;

  $: activeStream = data.streams.find(stream => stream.active);
</script>

<div>
  {#if activeStream}
    <!-- redirect -->
  {:else}
    <div>No active streams</div>
  {/if}
</div>
