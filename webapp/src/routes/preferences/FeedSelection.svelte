<script>
  import { fade } from "svelte/transition";
  import { streams, deleteStream, addStream as addStreamToStore } from "../../stores/streams";

  // export let streams = [];
  let streamToAdd = "";
  let isSubmitting = false;

  // subscribe to the streams store using shorthand syntax
  // $streams = streams;

  const validationRegex = /^(?:https:\/\/)*(?:www\.)*broadcastify\.com\/listen\/feed\/\d+$/g;
  const broadcastifyAnchor = '<a target="_blank" class="underline" href="https://www.broadcastify.com/listen/">Broadcastify</a>';

  function addStream() {
    isSubmitting = true;
    addStreamToStore(streamToAdd)
      .then(() => {
        streamToAdd = "";
      })
      .finally(() => {
        isSubmitting = false;
      });
  }


  $: isValidBroadcastifyUrl = !streamToAdd || validationRegex.test(streamToAdd);
</script>

<div class="card shadow-xl">
  <header class="card-header h3 font-bold mb-6">
    Radio Feeds
  </header>

  <section class="px-4">
    <ul class="divide-y divide-slate-500">
      {#each $streams as stream}
      <li class="py-4 flex justify-between items-center">
          <h3>{stream.title}</h3>
          <button on:click={deleteStream.bind(null, stream._id)} class="variant-soft">
            <i class="fas fa-trash text-lg" />
          </button>
        </li>
      {/each}
    </ul>
  </section>

  <hr />

  <footer class="card-footer mt-8">
    <form>
      <div class="input-group input-group-divider grid-cols-[auto_1fr_auto]">
        <div class="input-group-shim"><i class="fas fa-globe" /></div>
        <input bind:value={streamToAdd} class:input-error={!isValidBroadcastifyUrl} type="text" title="Broadcastify URL" placeholder="Broadcastify URL" />
        <button on:click={addStream} class="variant-filled-secondary"><i class="fas fa-plus pr-2 text-sm" />Add</button>
      </div>
      {#if isValidBroadcastifyUrl}
        <span in:fade class="text-xs text-slate-500">You can find a feed on {@html broadcastifyAnchor}.</span>
      {:else}
        <span in:fade class="text-xs text-error-500">Invalid Broadcastify URL</span>
      {/if}
    </form>
  </footer>
</div>
