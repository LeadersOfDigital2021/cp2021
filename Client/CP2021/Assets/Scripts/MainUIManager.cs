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

    private void Start()
    {
        OpenScreen(loginScreen);
    }

    private void OpenScreen(GameObject screen)
    {
        loginScreen.SetActive(screen == loginScreen);
        mainScreen.SetActive(screen == mainScreen);
        newRecord.SetActive(screen == newRecord);
        textRecorded.SetActive(screen == textRecorded);
        protocolScreen.SetActive(screen == protocolScreen);
    }

    public void OpenMainScreen()
    {
        OpenScreen(mainScreen);
    }

    public void OpenNewRecordScreen()
    {
        OpenScreen(newRecord);
    }

    public void OpenTextRecordedScreen()
    {
        OpenScreen(textRecorded);
    }

    public void OpenProtocolScreen()
    {
        OpenScreen(protocolScreen);
    }
}