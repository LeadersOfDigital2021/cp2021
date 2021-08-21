using System;
using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class Record : MonoBehaviour
{
    [SerializeField]
    private TMP_Text timerText;

    [SerializeField]
    private Sprite playSprite;

    [SerializeField]
    private Sprite pauseSprite;

    [SerializeField]
    private Button playButton;

    [SerializeField]
    private GameObject recordAttention;

    private bool isPlayed;
    private Coroutine timerCoroutine;
    private float timer;
    private string timerFormatted;

    private void Start()
    {
        recordAttention.SetActive(isPlayed);
    }

    public void StartRecord()
    {
        if (timerCoroutine != null)
        {
            StopCoroutine(timerCoroutine);
            timerCoroutine = null;
        }

        if (isPlayed)
        {
            isPlayed = false;
            playButton.image.sprite = playSprite;
        }
        else
        {
            isPlayed = true;
            timer = 0f;
            playButton.image.sprite = pauseSprite;
            timerCoroutine = StartCoroutine(Timer());
        }
        recordAttention.SetActive(isPlayed);
    }

    private IEnumerator Timer()
    {
        while (isPlayed)
        {
            timer += Time.deltaTime;
            System.TimeSpan t = System.TimeSpan.FromSeconds(timer);
            timerFormatted = string.Format("{0:D2}:{1:D2}:{2:D2}", t.Hours, t.Minutes, t.Seconds);
            timerText.text = timerFormatted;
            yield return null;
        }
    }
}