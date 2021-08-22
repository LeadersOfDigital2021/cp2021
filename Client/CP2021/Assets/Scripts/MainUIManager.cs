using System;
using UnityEngine;

public class MainUIManager : MonoBehaviour
{
    [SerializeField]
    private GameObject loginScreen;

    [SerializeField]
    private GameObject mainScreen;

    [SerializeField]
    private GameObject newRecord;

    [SerializeField]
    private GameObject textRecorded;

    [SerializeField]
    private GameObject protocolScreen;

    [SerializeField]
    private GameObject uploadScreen;

    [SerializeField]
    private CanvasSampleOpenFileText firstFileLoader;

    [SerializeField]
    private GameObject speech;

    [SerializeField]
    private Transform content;

    private void Start()
    {
        firstFileLoader.FileLoaded += OnFileLoaded;
        OpenScreen(loginScreen);
    }

    private void OnFileLoaded(Byte[] bytes)
    {
        OpenTextRecordedScreen();
    }

    private void OpenScreen(GameObject screen)
    {
        loginScreen.SetActive(screen == loginScreen);
        mainScreen.SetActive(screen == mainScreen);
        newRecord.SetActive(screen == newRecord);
        textRecorded.SetActive(screen == textRecorded);
        protocolScreen.SetActive(screen == protocolScreen);
        uploadScreen.SetActive(screen == uploadScreen);
    }

    public void OpenMainScreen()
    {
        OpenScreen(mainScreen);
    }

    public void OpenNewRecordScreen()
    {
        OpenScreen(newRecord);
        speech.SetActive(true);
        content.localPosition = Vector3.zero;
    }

    public void OpenTextRecordedScreen()
    {
        OpenScreen(textRecorded);
    }

    public void OpenProtocolScreen()
    {
        OpenScreen(protocolScreen);
    }

    public void OpenUploadScreen()
    {
        uploadScreen.SetActive(true);
    }
}