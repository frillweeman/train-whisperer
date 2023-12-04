<script>
  export let color = "primary";
  export let disabled = false;
  export let outlined = false;
  export let joined = false;
  export let square = false;
  export let ghost = false;

  $: colorClass = `btn-${color}`
</script>

<button
  on:click
  class="btn {colorClass}"
  class:btn-disabled={disabled}
  class:btn-outline={outlined}
  class:join-item={joined}
  class:btn-square={square}
  class:btn-ghost={ghost}
>
  <slot />
</button>
