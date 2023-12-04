<script>
  import TextField from '$lib/global-components/TextField.svelte';
  import Button from '$lib/global-components/Button.svelte';

  export let streams = [];
  export let streamToAdd = "";

  const validationRegex = /^(?:https:\/\/)*(?:www\.)*broadcastify\.com\/listen\/feed\/\d{4}$/g;
  const broadcastifyAnchor = '<a target="_blank" class="link" href="https://www.broadcastify.com/listen/">Broadcastify</a>';

  function handleClick() {
    console.log('clicked');
  }
</script>

<div class="card shadow-xl bg-base-100">
  <div class="card-body">
    <h2 class="card-title">Manage Radio Feeds</h2>

    <ul class="divide-y divide-slate-300">
      {#each streams as stream}
      <li class="py-4 flex justify-between items-center">
          <h3>{stream.title}</h3>
          <Button ghost>
            <svg class="h-6 fill-black dark:fill-slate-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>delete</title><path d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z" /></svg>
          </Button>
        </li>
      {/each}
    </ul>

    <form class="card-actions">
      <div class="join w-full">
        <TextField bind:value={streamToAdd} joined bordered placeholder="Broadcastify URL" hint="You can add a feed from {broadcastifyAnchor}" {validationRegex} />
        <Button disabled={!streamToAdd} joined outlined color="primary" on:click={handleClick}>Add URL</Button>
      </div>
    </form>
  </div>
</div>
