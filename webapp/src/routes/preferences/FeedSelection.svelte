<script>
  import TextField from '$lib/global-components/TextField.svelte';
  import Button from '$lib/global-components/Button.svelte';
  import { fade } from "svelte/transition";

  export let streams = [];
  export let streamToAdd = "";
  
  let isValidBroadcastifyUrl = true;

  const validationRegex = /^(?:https:\/\/)*(?:www\.)*broadcastify\.com\/listen\/feed\/\d{4}$/g;
  const broadcastifyAnchor = '<a target="_blank" class="underline" href="https://www.broadcastify.com/listen/">Broadcastify</a>';

  function handleClick() {
    console.log('clicked');
  }
  function validate({ target }) {
    const { value } = target;
    isValidBroadcastifyUrl = !value || validationRegex.test(value);
  }
</script>

<div class="card shadow-xl">
  <header class="card-header h3 font-bold mb-6">
    Radio Feeds
  </header>

  <section class="px-4">
    <ul class="divide-y divide-slate-500">
      {#each streams as stream}
      <li class="py-4 flex justify-between items-center">
          <h3>
            {stream.title}
          </h3>
          <span>
            {#if stream.channels > 1}
              <div class="mx-2 text-xs font-bold chip variant-filled-surface">
                <i class="fas fa-microphone" />
                <span>x2</span>
              </div>
            {/if}
            <Button variant="soft">
              <i class="fas fa-trash text-lg" />
            </Button>
          </span>
        </li>
      {/each}
    </ul>
  </section>

  <hr />

  <footer class="card-footer mt-8">
    <!-- <form> -->
      <div class="input-group input-group-divider grid-cols-[auto_1fr_auto]">
        <div class="input-group-shim"><i class="fas fa-globe" /></div>
        <input on:input={validate} class:input-error={!isValidBroadcastifyUrl} type="text" title="Broadcastify URL" placeholder="Broadcastify URL" />
        <button class="variant-filled-secondary"><i class="fas fa-plus pr-2 text-sm" />Add</button>
      </div>
      {#if isValidBroadcastifyUrl}
        <span in:fade class="text-xs text-slate-500">You can find a feed on {@html broadcastifyAnchor}.</span>
      {:else}
        <span in:fade class="text-xs text-error-500">Invalid Broadcastify URL</span>
      {/if}
    <!-- </form> -->
  </footer>
</div>
