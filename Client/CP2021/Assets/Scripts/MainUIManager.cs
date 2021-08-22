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

    [SerializeField]
    private GameObject protocol1;

    [SerializeField]
    private GameObject protocol2;

    private void Start()
    {
        firstFileLoader.FileLoaded += OnFileLoaded;
        OpenScreen(loginScreen);
    }

    private void OnFileLoaded()
    {
        protocol1.SetActive(true);
        protocol2.SetActive(false);
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

        protocol2.SetActive(true);
        protocol1.SetActive(false);
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